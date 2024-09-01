## https://k6.io/docs/get-started/installation/

### Debian/Ubuntu

 ```
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

or

snap install k6
 ```


#### Run K6 player load test script
 ```
 k6 run ac.js
 ```
### Debug mode
To enable the debug mode put the following parameter into the command line
 ```
--http-debug="full"
 ```
