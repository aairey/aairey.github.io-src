# aairey.github.io-src
Source for the website at [aairey.github.io](http://aairey.github.io).

## Dependencies

Tested with Pelican v3.7.1.

## Installing

    cd ~/git_projects
    git clone git@github.com:aairey/aairey.github.io-src.git
    cd aairey.github.io-src
    mkvirtualenv pelican
    pip install pelican markdown disqus-python
    git submodule update --init --recursive

## Creating posts

Create all posts in the `content/` folder in Markdown format.

## Testing new content

    make html && make serve

## Publishing content

    make publish
    cd output
    git add .
    git commit -m "New Post"
    git push
    cd ..
    git add .
    git commit -m "Created New Post"
    git push

