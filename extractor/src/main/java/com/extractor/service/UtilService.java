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
public class UtilService {

    static final Logger logger = LoggerFactory.getLogger(ConvertService.class);

    public byte[] multipartFileToByteArray(MultipartFile file) {
        try {
            return file.getBytes();
        } catch (Exception e) {
            logger.error("multipartFileToByteArray: Could not get byte array from MultiPartFile", e);
        }
        return null;
    }
}