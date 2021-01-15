package com.extractor.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class Page {
    private String text;
    private int pageNumber;
}
