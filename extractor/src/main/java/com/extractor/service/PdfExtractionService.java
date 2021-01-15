package com.extractor.service;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import com.extractor.model.PDF;
import com.extractor.model.Page;
import org.apache.pdfbox.multipdf.Splitter;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDDocumentInformation;
import org.apache.pdfbox.text.PDFTextStripper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class PdfExtractionService {

    @Autowired
    ConvertService convertService;

    static final Logger logger = LoggerFactory.getLogger(ConvertService.class);

    public PDF extract(MultipartFile multipartFile) {
        byte[] bytes = convertService.multipartFileToByteArray(multipartFile);
        PDDocument document = getPDDocumentFromByteArray(bytes);
        PDF pdf = new PDF();
        addText(document, pdf);
        addMetaData(document, pdf);
        try {
            document.close();
        } catch (IOException e) {
            logger.error("extract: Couldn't close PDDocument", e);
        }
        return pdf;
    }

    public void addText(PDDocument document, PDF pdf) {
        if (document == null) {
            return;
        }

        try {
            PDFTextStripper pdfStripper = new PDFTextStripper();
            Splitter splitter = new Splitter();
            List<PDDocument> pages = splitter.split(document);
            int pageNumber = 1;
            for (PDDocument doc : pages) {
                Page page = new Page();
                String text = pdfStripper
                        .getText(doc)
                        .replaceAll("(\\r\\n)|(\\n)", " ")
                        .replaceAll(" +", " ")
                        .trim();
                page.setText(text);
                if (text == null || text.isEmpty()) continue;
                page.setPageNumber(pageNumber++);
                pdf.addPage(page);
                doc.close();
            }
        } catch (IOException e) {
            logger.error("addText: Could not parse PDDocument", e);
        }
    }

    public void addMetaData(PDDocument document, PDF pdf) {
        if (document == null) {
            return;
        }
        PDDocumentInformation info = document.getDocumentInformation();
        pdf.setTitle(info.getTitle());
        pdf.setAuthor(info.getAuthor());
        pdf.setSubject(info.getSubject());
        pdf.setKeywords(info.getKeywords());
        pdf.setNumberOfPages(pdf.getPages().size());
        pdf.setCreationDate(info.getCreationDate());
        pdf.setModificationDate(info.getModificationDate());
    }

    public PDDocument getPDDocumentFromByteArray(byte[] bytes) {
        try {
            InputStream documentStream = new ByteArrayInputStream(bytes);
            return PDDocument.load(documentStream);
        } catch (IOException e) {
            logger.error("getPDDocumentFromByteArray: Could not load PDDocument from byte array", e);
        }
        return null;
    }
}
