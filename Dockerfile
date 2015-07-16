FROM centos

RUN yum -y install gettext python; yum clean all
ADD *.py *.sh /usr/bin/
