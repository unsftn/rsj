FROM maven:3.8.2-openjdk-8 AS MAVEN_BUILD
RUN mkdir /app
COPY pom.xml /app
COPY src /app/src
WORKDIR /app
# RUN mvn clean install -B -Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer.Slf4jMavenTransferListener=warn
RUN mvn clean package spring-boot:repackage -B -Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer.Slf4jMavenTransferListener=warn

FROM openjdk:8
COPY --from=MAVEN_BUILD /app/target/extractor.jar /extractor.jar
EXPOSE 8090
CMD ["java", "-jar", "/extractor.jar"]
