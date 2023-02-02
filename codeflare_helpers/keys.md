# Configure your Clowder authentication
=== "ONE Enter your Clowder hostname (e.g. http://localhost:8000, or https://pdg.clowderframework.org) [default: your_hostname_or_url]"
    details here.
    ```shell
    export CLOWDER_HOSTNAME=${choice}
    ```

# Clowder API key
=== "TWO Enter your Clowder API key (found in View Profile -> API Keys) e.g. bbe2dce9-c3eb... [default: your_API_key]"
    details here.
    ```shell
    export CLOWDER_API_KEY=${choice}
    ```


```shell
if [ ! -d ~/.clowder ]; then mkdir ~/.clowder; fi
cat << EOF > ~/.clowder/credentials
[CodeFlare created Clowder hostname and API key]
${CLOWDER_HOSTNAME}
${CLOWDER_API_KEY}
EOF
```
