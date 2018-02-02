# docker-registry-gitlab-cleanup

The goal of this tool is to be able to cleanup old image tags stored in a [GitLab](http://gitlab.org/) embedded [Docker Registry](https://docs.docker.com/registry/).

# Prerequisites

- GitLab version 10.2 or above
- Docker Registry version 2.3 or above
- Have an administrator account onto the GitLab server
- Be able to reach both GitLab and Docker registry endpoint APIs from the same location.
- [Generate a token](https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html) with `api` and `sudo` privileges

# Usage

```bash
docker run -it --rm \
  -e RGC_USER=<username> \
  -e RGC_TOKEN=<token> \
  -e RGC_GITLAB_URL=https://gitlab.example.com \
  -e RGC_REGISTRY_URL=https://registry.gitlab.example.com \
  mvisonneau/docker-registry-gitlab-cleanup
```

You should then have something like this :

```bash
-> loading all projects..
-> processing mynamespace/myproject
--> 43 tag(s) found
--> removing 05060832769b138a61ff5f1a4e8134b4d041029f (expired)
--> keeping 09d7b5f8cfa93c9066120b3b3c3b90941be25596 (not expired)
--> removing 1318c013ad28e6296dca605d0645a4cd66bd2733 (expired)
--> keeping 187980e653e42344471dc6be179571cdc97a6a3a (not expired)
--> removing 1d8266a16d54e608a14f5988fdc94a983f5a8fcd (expired)
--> keeping 2a96e6ac72a7946253b620fc9ec0e48b0afc36d8 (not expired)
--> removing 399cd8f39ffe242543046a37e6ea98f09926d2b6 (expired)
--> removing 3ebc19cb82261eb1ebee10218e95deea674aab7c (expired)
--> removing 4ca424ff3be622fe4a20a0e2dfc6443881618ade (expired)
--> removing 53f50a76177b561a88bc709fa304dafa76a06a46 (expired)
[..]
```

# Known issues

Even though it does actually clean the registry, it doesn't remove the blobs. You should then run the [garbage collector](https://docs.gitlab.com/omnibus/maintenance/README.html#container-registry-garbage-collection) do to so.

## Develop / Test

```bash
~$ git clone https://github.com/mvisonneau/docker-registry-gitlab-cleanup
~$ docker build -t <your_namespace>/docker-registry-gitlab-cleanup .
~$ docker run -it --rm <your_namespace>/docker-registry-gitlab-cleanup sh
~$ rgc
```

## Contribute

Contributions are more than welcome! Feel free to submit a [PR](https://github.com/mvisonneau/docker-registry-gitlab-cleanup/pulls).
