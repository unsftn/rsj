package com.extractor.model;

import com.extractor.util.DateConverter;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import java.util.*;

@Getter
@Setter
public class PDF {
    private String author;
    private String title;
    private String subject;
    private String keywords;
    private int numberOfPages;
    private String creationDate;
    private String modificationDate;
    private List<Page> pages;

    public PDF() {
        pages = new ArrayList<>();
    }

    public void addPage(Page page) {
        if (pages == null) {
            pages = new ArrayList<>();
        }
        pages.add(page);
    }

    public void setCreationDate(Calendar date) {
        this.creationDate = DateConverter.convertCalendarToISO8601(date);
    }

    public void setCreationDate(Date date) {
        this.creationDate = DateConverter.convertDateToISO8601(date);
    }

    public void setModificationDate(Calendar date) {
        this.modificationDate = DateConverter.convertCalendarToISO8601(date);
    }

    public void setModificationDate(Date date) {
        this.modificationDate = DateConverter.convertDateToISO8601(date);
    }
}