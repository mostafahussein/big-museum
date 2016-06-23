docker build --force-rm -t big-museum-test .
docker run -p 8000:80 -i big-museum-test