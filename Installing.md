## Installing ovirt-engine-sdk-python

1. Install brew and hange homebrew repo https://blog.csdn.net/lwplwf/article/details/79097565

2. Install pip

~~~
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
~~~ 

3. Install MacOS headers in order to install libxml headers
~~~
  # sudo xcode-select --install
  # sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
~~~

4. Enable virtualenv
~~~
  # pip install virtualenv
  # mkdir ~/virtenv
  # cd ~/virtenv
  # virtualenv titamu ## You can change the directory name as you want
  # cd titamu
  # source bin/activate
  ## The method to quit virtualenv
  # source bin/deactivate
~~~

5. Install pycurl pretty table and sdk inside virtualenv
~~~
  # pip install pycurl prettytable ovirt-engine-sdk-python
~~~

6. If there is any errors installing pycurl, try the following
~~~
  # export PYCURL_SSL_LIBRARY=openssl
  # export LDFLAGS="-L/usr/local/opt/openssl/lib"
  # export CPPFLAGS="-I/usr/local/opt/openssl/include"
  # brew install openssl
~~~

7. Download ca.pem
~~~
  # wget 'lab-rhevm.gsslab.pek2.redhat.com/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA' --no-check-certificate
  # mv  pki-resource\?resource\=ca-certificate\&format\=X509-PEM-CA ca.pem
~~~

8. Have fun with sample code https://github.com/oVirt/ovirt-engine-sdk/blob/master/sdk/examples/list_vms.py
