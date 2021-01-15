package com.extractor.service;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.slf4j.LoggerFactory;

@Service
public class ConvertService {

    @Autowired
    PdfExtractionService pdfExtractionService;

    static final Logger logger = LoggerFactory.getLogger(ConvertService.class);

    public PDDocument wordToPDF(MultipartFile multipartFile) {
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            HttpEntity entity = MultipartEntityBuilder.create().setMode(
                    HttpMultipartMode.BROWSER_COMPATIBLE).setBoundary("----WebKitFormBoundaryDeC2E3iWbTv1PwMC").setContentType(
                    ContentType.MULTIPART_FORM_DATA)
                    .addBinaryBody("files",
                            multipartFile.getBytes(),
                            ContentType.MULTIPART_FORM_DATA, multipartFile.getOriginalFilename())
                    .addTextBody("waitTimeout", "30", ContentType.MULTIPART_FORM_DATA)
                    .build();

            HttpPost httpPost = new HttpPost("http://gotenberg:3000/convert/office");
            httpPost.setEntity(entity);
            HttpResponse response = httpClient.execute(httpPost);
            byte[] responseBody = EntityUtils.toByteArray(response.getEntity());
            httpClient.close();
            return pdfExtractionService.getPDDocumentFromByteArray(responseBody);
        } catch (Exception e) {
            logger.error("wordToPDF: Conversion failed with error: ", e);
        }
        return null;
    }

    public byte[] multipartFileToByteArray(MultipartFile file) {
        try {
            return file.getBytes();
        } catch (Exception e) {
            logger.error("multipartFileToByteArray: Could not get byte array from MultiPartFile", e);
        }
        return null;
    }
}