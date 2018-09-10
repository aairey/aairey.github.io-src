# aairey.github.io-src
Source for the website at [aairey.github.io](http://aairey.github.io) / [blog.airey.be](https://blog.airey.be/).

## Dependencies

Tested with Pelican v3.7.1.

## Installing

```bash
cd ~/git_projects
git clone git@github.com:aairey/aairey.github.io-src.git
cd aairey.github.io-src
mkvirtualenv pelican
pip install -r requirements.txt
git submodule update --init --recursive
```

## Creating posts

Create all posts in the `content/` folder in Markdown format.

## Testing new content

```bash
make html && make serve
```

## Publishing content

```bash
make github
```
