FROM centos

RUN yum -y install gettext python; yum clean all
ADD analyze-po-files.py /usr/bin/
