package com.extractor.service;

import com.extractor.model.PDF;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.poi.POIXMLProperties;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.IOException;

@Service
public class WordExtractionService {

    @Autowired
    PdfExtractionService pdfExtractionService;

    @Autowired
    ConvertService convertService;

    static final Logger logger = LoggerFactory.getLogger(ConvertService.class);

    public PDF extract(MultipartFile multipartFile) {
        byte[] bytes = convertService.multipartFileToByteArray(multipartFile);
        PDF pdf = new PDF();
        XWPFDocument wordDocument = getXWPFDocumentFromByteArray(bytes);
        PDDocument pdfDocument = convertService.wordToPDF(multipartFile);
        pdfExtractionService.addText(pdfDocument, pdf);
        addMetaData(wordDocument, pdf);
        try {
            pdfDocument.close();
            wordDocument.close();
        } catch (IOException e) {
            logger.error("extract: Couldn't close PDDocument or wordDocument", e);
        }
        return pdf;
    }

    private void addMetaData(XWPFDocument document, PDF pdf) {
        if (document == null) {
            return;
        }
        POIXMLProperties prop = document.getProperties();
        POIXMLProperties.CoreProperties coreProps = prop.getCoreProperties();
        pdf.setAuthor(coreProps.getCreator());
        pdf.setKeywords(coreProps.getKeywords());
        pdf.setCreationDate(coreProps.getCreated());
        pdf.setTitle(coreProps.getTitle());
        pdf.setSubject(coreProps.getSubject());
        pdf.setModificationDate(coreProps.getModified());
        if (pdf.getPages() != null) {
            pdf.setNumberOfPages(pdf.getPages().size());
        }
    }

    private XWPFDocument getXWPFDocumentFromByteArray(byte[] bytes) {
        try {
            return new XWPFDocument(new ByteArrayInputStream(bytes));
        } catch (Exception e) {
            logger.error("getXWPFDocumentFromByteArray: Could not convert byte array into XWPFDocument", e);
        }
        return null;
    }
}
