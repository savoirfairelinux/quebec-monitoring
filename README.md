quebec-monitoring
=================

Dockerfile all-in-the-box, plugins and templates to monitor various metrics in Québec.

Let's monitor Quebec! This work is inspired by
http://iceland.adagios.org by @palli.


## How to: run at home

The only dependency is Docker, on Debian- or Ubuntu-based distros you
can:
```
$ sudo apt-get install docker.io
```

After cloning the repository, just do:
```
$ sudo make run
```

If you installed Docker manually, perhaps the command to run it is
`docker` instead of `docker.io`. In this case, run `sed -i
s/docker.io/docker/g Makefile`

And now, navigate to your container IP. In order to know your
container IP, you can run `sudo docker.io inspect <container-number>`,
replacing <container-number> by the last line returned by the previous
command.

<dl>
  <dt>What? You really use sudo? This looks dangerous.</dt>
  <dd>Admin rights are required to use Docker. If you're not confident
  doing this, you can easily check that no OS image is downloaded,
  everything is built in the Dockerfile.</dd>

  <dt>Is it really that simple to run?</dt>
  <dd>Yes.</dd>
</dl>


## How to: contribute

Everything here is based on:
* back-end: the monitoring engine Shinken,
* front-end: the Django applicatin Adagios,
* all-in-the-box: the container manager Docker.

If you want to add a metric in an existing category, you can add
relevant information in scripts/<category>.py.

If you want to create a new category, add a script in
scripts/<your-cool-idea>.py, and a line in the Makefile.

__Pull requests, patches, bug reports, feedback and pizzas are always
welcome!__
 