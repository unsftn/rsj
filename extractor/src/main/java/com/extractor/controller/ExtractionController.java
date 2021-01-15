package com.extractor.controller;

import com.extractor.service.PdfExtractionService;
import com.extractor.service.WordExtractionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/extract")
public class ExtractionController {

    @Autowired
    private PdfExtractionService pdfExtractionService;

    @Autowired
    private WordExtractionService wordExtractionService;

    @RequestMapping(method=RequestMethod.POST, produces = "application/json; charset=UTF-8")
    public ResponseEntity<?> extractText(@RequestParam("file") MultipartFile multipartFile) {
        if (multipartFile == null) {
            return new ResponseEntity<>("\"file\" is required field.", HttpStatus.BAD_REQUEST);
        }
        String fileName = multipartFile.getOriginalFilename();
        if (fileName.endsWith("docx")) {

            return new ResponseEntity<>(wordExtractionService.extract(multipartFile), HttpStatus.OK);
        }
        else if (fileName.endsWith("pdf")) {

            return new ResponseEntity<>(pdfExtractionService.extract(multipartFile), HttpStatus.OK);
        }

        return new ResponseEntity<>("File must be Microsoft Word document or PDF.", HttpStatus.BAD_REQUEST);
    }
}