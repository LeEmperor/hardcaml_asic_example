"""Actual consumer executable, synthetic provenance and recording provider; no EDA."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest
import venv

EXE, EXPORTER, SOURCE = [Path(p).resolve() for p in sys.argv[1:4]]
sys.argv[1:] = []


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="fifo-routing-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "TOOLCHAIN"}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Bundle test", GIT_AUTHOR_EMAIL="bundle@test.invalid",
                        GIT_COMMITTER_NAME="Bundle test", GIT_COMMITTER_EMAIL="bundle@test.invalid",
                        GIT_AUTHOR_DATE="2026-01-01T00:00:00Z", GIT_COMMITTER_DATE="2026-01-01T00:00:00Z")
        inputs = subprocess.check_output([str(EXPORTER), "--inputs"], env=self.env, text=True).splitlines()
        for name in inputs:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, dest)
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), "-c", "core.hooksPath=/dev/null",
                "-c", "commit.gpgsign=false", "-c", "init.templateDir=", *args], env=self.env, text=True).strip()
        git("init", "--initial-branch=fixture")
        git("add", ".")
        git("commit", "-m", "baseline")
        self.assertEqual(git("show", "-s", "--format=%an <%ae>|%cn <%ce>"),
                         "Bundle test <bundle@test.invalid>|Bundle test <bundle@test.invalid>")
        self.assertEqual(git("remote"), "")
        self.nested = self.root / "nested" / "deeper"
        self.nested.mkdir(parents=True)
        self.outside = self.base / "outside"
        self.outside.mkdir()
        self.providers = self.base / "providers"
        self.providers.mkdir()
        self.log = self.base / "calls.jsonl"
        provider = self.providers / "hardcaml-asic-flow"
        provider.write_text(f"#!{sys.executable}\n" + '''import json, os, sys
if '--version' in sys.argv:
    print(json.dumps({'cli_contract': {'version': int(os.environ.get('CONTRACT', '2'))}}))
else:
    with open(os.environ['RECORD'], 'a') as f:
        f.write(json.dumps({'argv': sys.argv[1:], 'cwd': os.getcwd(), 'executable': sys.argv[0]}) + '\\n')
    print(json.dumps({'recorded': True}) if '--json' in sys.argv else 'Recorded implementation dispatch')
    if '--verbose' in sys.argv: print('provider diagnostic', file=sys.stderr)
    if os.environ.get('PROVIDER_SIGNAL'): os.kill(os.getpid(), int(os.environ['PROVIDER_SIGNAL']))
    sys.exit(int(os.environ.get('PROVIDER_EXIT', '0')))
''')
        provider.chmod(0o755)
        self.env.update(PATH=str(self.providers) + os.pathsep + self.env.get("PATH", ""), RECORD=str(self.log))

    def invoke(self, *args, cwd=None, status=0, env=None):
        result = subprocess.run([str(EXE), *args], cwd=cwd or self.nested, env=env or self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, status, (args, result.stdout, result.stderr))
        return result

    def call(self):
        return json.loads(self.log.read_text().splitlines()[-1])

    def test_default_emit_reuse_and_corruption(self):
        first = json.loads(self.invoke("emit", "--json").stdout)
        path = Path(first['output_dir'])
        self.assertEqual(path.parent, self.root / '_flow_results/bundles')
        self.assertTrue(path.is_symlink())
        self.assertEqual(path.resolve().parent, path.parent / '.objects')
        self.assertEqual(json.loads(self.invoke('emit', '--json', '--verbose').stdout), first)
        self.assertIn('Reused', self.invoke('emit').stdout)
        manifest = path / 'manifest.json'
        manifest.write_text('corrupt')
        self.invoke('emit', '--json', status=1)
        self.assertEqual(manifest.read_text(), 'corrupt')

    def test_explicit_roots_and_exact_output(self):
        response = json.loads(self.invoke('emit', '--project-root', '../project', '--source-root', '../project',
            '--results-root', 'results', '--json', cwd=self.outside).stdout)
        self.assertEqual(Path(response['output_dir']).parent, self.outside / 'results/bundles')
        exact = json.loads(self.invoke('emit', '--source-root', '../project', '--output-dir', 'exact',
            '--json', cwd=self.outside).stdout)
        self.assertEqual(exact['output_dir'], str(self.outside / 'exact'))
        self.assertFalse(Path(exact['output_dir']).is_symlink())

    def test_validation_and_readonly(self):
        for args in [('run',), ('run', '--stage', 'invalid'),
                     ('emit', '--project-root', str(self.root), '--source-root', str(self.outside)),
                     ('run', '--stage', 'full', '--bogus'),
                     ('preflight', '--python', '--json'), ('emit', '--results-root', '')]:
            self.invoke(*args, status=2)
        self.invoke('emit', cwd=self.outside, status=2)
        generated = self.root / '_build/default'
        generated.mkdir(parents=True)
        self.invoke('emit', cwd=generated, status=2)
        self.assertFalse((self.root / '_flow_results').exists())
        self.assertFalse(self.log.exists())
        for command in ['describe', 'emit', 'preflight', 'run']:
            self.invoke(command, '--help', cwd=self.outside)
        self.invoke('describe', '--json', cwd=self.outside)
        self.assertFalse((self.root / '_flow_results').exists())
        (self.root / 'bin/project.ml').unlink()
        self.invoke('emit', status=2)
        self.assertFalse((self.root / '_flow_results').exists())

    def test_default_dispatch_json_and_current_source(self):
        response = self.invoke('preflight', '--json', '--verbose')
        self.assertEqual(json.loads(response.stdout), {'recorded': True})
        self.assertIn('provider diagnostic', response.stderr)
        call = self.call()
        argv = call['argv']
        self.assertEqual(call['cwd'], str(self.nested))
        self.assertEqual(argv[0], 'preflight')
        self.assertEqual(argv[2:], ['--results-root', str(self.root / '_flow_results'),
            '--toolchain', str(self.root / '_flow_tools'), '--json', '--verbose'])
        first = argv[1]
        with (self.root / 'README.md').open('a') as f: f.write('\nchanged source\n')
        self.invoke('run', '--stage', 'synthesis', '--json')
        self.assertNotEqual(self.call()['argv'][1], first)
        self.assertEqual(len(self.log.read_text().splitlines()), 2)  # no duplicated preflight

    def test_overrides_exit_and_explicit_bundle(self):
        env = dict(self.env, TOOLCHAIN='env tools', PROVIDER_EXIT='37')
        self.invoke('run', '--bundle', 'bundle', '--stage', 'full', '--results-root', 'results',
            '--runs', 'runs', '--toolchain', 'explicit tools', '--python', 'python',
            '--support-tools', 'support', '--pdk-root', 'pdk', '--native', '--json',
            cwd=self.outside, env=env, status=37, *['--project-root', str(self.root)])
        argv = self.call()['argv']
        self.assertEqual(argv, ['run', str(self.outside / 'bundle'), '--results-root', str(self.outside / 'results'),
            '--toolchain', str(self.outside / 'explicit tools'), '--python', str(self.outside / 'python'),
            '--support-tools', str(self.outside / 'support'), '--pdk-root', str(self.outside / 'pdk'),
            '--runs', str(self.outside / 'runs'), '--stage', 'full', '--native', '--json'])
        self.assertFalse((self.root / '_flow_results').exists())
        self.invoke('preflight', '--bundle', 'bundle', '--output', 'report.json', env=dict(self.env, TOOLCHAIN='env tools'))
        argv = self.call()['argv']
        self.assertEqual(argv[argv.index('--toolchain') + 1], str(self.nested / 'env tools'))
        self.assertEqual(argv[argv.index('--output') + 1], str(self.nested / 'report.json'))

    def test_missing_and_old_provider_no_emission(self):
        result = self.invoke('preflight', env=dict(self.env, PATH=''), status=1)
        self.assertIn('install/activate', result.stderr)
        result = self.invoke('preflight', env=dict(self.env, CONTRACT='1'), status=1)
        self.assertIn('CLI contract 2', result.stderr)
        self.assertFalse((self.root / '_flow_results').exists())
        self.assertFalse(self.log.exists())

    def test_directory_paths_preserve_symlink_parent_traversal(self):
        child = self.root / 'child'
        child.mkdir()
        (self.outside / 'alias').symlink_to(child, target_is_directory=True)
        for name in ('bundle', 'tools', 'support', 'pdk'):
            (self.root / name).mkdir()
        self.invoke('preflight', '--project-root', 'alias/..', '--source-root', str(self.root),
                    '--bundle', 'alias/../bundle', '--toolchain', 'alias/../tools',
                    '--support-tools', 'alias/../support', '--pdk-root', 'alias/../pdk',
                    '--results-root', 'alias/../results', '--output', 'alias/../report.json',
                    cwd=self.outside)
        argv = self.call()['argv']
        self.assertTrue(os.path.samefile(argv[1], self.root / 'bundle'))
        for flag, name in (('--toolchain', 'tools'), ('--support-tools', 'support'), ('--pdk-root', 'pdk')):
            self.assertTrue(os.path.samefile(argv[argv.index(flag) + 1], self.root / name))
        for flag, name in (('--results-root', 'results'), ('--output', 'report.json')):
            self.assertEqual(argv[argv.index(flag) + 1], str(self.outside / ('alias/../' + name)))
        response = json.loads(self.invoke('emit', '--source-root', 'alias/..',
            '--output-dir', 'alias/../exact', '--json', cwd=self.outside).stdout)
        self.assertTrue(os.path.samefile(response['output_dir'], self.root / 'exact'))
        self.assertFalse((self.outside / 'exact').exists())

    def test_provider_signal_is_preserved(self):
        self.invoke('run', '--stage', 'synthesis', '--bundle', 'unused',
                    env=dict(self.env, PROVIDER_SIGNAL=str(signal.SIGTERM)), status=-signal.SIGTERM)
        self.assertFalse((self.root / '_flow_results').exists())

    def test_executable_paths_preserve_symlink_parent_traversal(self):
        real = self.base / 'real'
        (real / 'child').mkdir(parents=True)
        (self.outside / 'alias').symlink_to(real / 'child', target_is_directory=True)
        provider_dir = real / 'providers'
        provider_dir.mkdir()
        shutil.copyfile(self.providers / 'hardcaml-asic-flow', provider_dir / 'hardcaml-asic-flow')
        (provider_dir / 'hardcaml-asic-flow').chmod(0o755)
        env = dict(self.env, PATH='alias/../providers')
        python_dir = real / 'venv'
        venv.EnvBuilder(with_pip=False, symlinks=True).create(python_dir)
        for python in ('alias/../venv/bin/python', str(self.outside / 'alias/../venv/bin/python')):
            with self.subTest(python=python):
                self.invoke('preflight', '--project-root', str(self.root), '--bundle', 'unused',
                            '--python', python, '--json', cwd=self.outside, env=env)
                call = self.call()
                intended = str(self.outside / 'alias/../venv/bin/python')
                forwarded = call['argv'][call['argv'].index('--python') + 1]
                self.assertEqual(forwarded, intended)
                self.assertEqual(call['executable'], str(self.outside / 'alias/../providers/hardcaml-asic-flow'))
                self.assertFalse((self.outside / 'venv').exists())
                self.assertTrue(os.path.samefile(Path(forwarded).parent.parent / 'pyvenv.cfg',
                                                python_dir / 'pyvenv.cfg'))
        prefix = subprocess.check_output([str(python_dir / 'bin/python'), '-c',
                                          'import sys; print(sys.prefix)'], text=True).strip()
        self.assertEqual(Path(prefix).resolve(), python_dir)
        self.assertFalse((self.root / '_flow_results').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
