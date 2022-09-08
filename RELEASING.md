# Release Checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/hugovk/pepotron/actions) should be running
      cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/hugovk/pepotron/workflows/Test/badge.svg)](https://github.com/hugovk/pepotron/actions)

- [ ] Edit release draft, adjust text if needed:
      https://github.com/hugovk/pepotron/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/hugovk/pepotron/actions/workflows/deploy.yml)
      has deployed to [PyPI](https://pypi.org/project/pepotron/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y pepotron && pip3 install -U pepotron && pep --version
```
