#Run your file
buildImage:
	docker build . -t "${USER}"/cursos
runImage:
	docker run -p 8080:8080 -d "${USER}"/cursos

buildDC:
	docker-compose build --no-cache
runDC:
	docker-compose up -d