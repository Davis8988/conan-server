
FROM conanio/conan_server:1.32.1
LABEL maintainer="david.yair@elbitsystems.com"
LABEL description="This Dockerfile just adds permissions, username & password configuration \
to the conan-server docker image created by: 'conanio/conan_server'"

ADD . /conan-1.32.1


