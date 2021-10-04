FROM maven:3.8.2-openjdk-8 AS MAVEN_BUILD
RUN mkdir /app
COPY pom.xml src /app
WORKDIR /app
RUN mvn -e clean install

FROM openjdk:8
COPY --from=MAVEN_BUILD /app/target/extractor.jar /extractor.jar
CMD ["java", "-jar", "extractor.jar"]
