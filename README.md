# YASBE
Yet Another Static Blog Engine 
[(Demo)](http://yasbe.surge.sh/)

Unlike others Static Blogs Generators like Pelican or Jekyll, this one was made to be modified, 
so don't expect to get cool themes, ready "plugins" or anything.

That's my special way to tell that I'm lazy.

## Dependencies

* python3
* [Mako](http://www.makotemplates.org/)
* [toml](https://pypi.python.org/pypi/toml)
* [mistune](https://github.com/lepture/mistune)

## Installing

* clone this repo
* copy `config_ex.toml` to `config.toml`
* install deps
* run `make serve`
* access [localhost:4000](http://localhost:4000)

Your blog will be available at the `www` directory.