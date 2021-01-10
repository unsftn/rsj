import { TestBed } from '@angular/core/testing';

import { StaticHtmlService } from './static-html.service';

describe('StaticHtmlService', () => {
  let service: StaticHtmlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StaticHtmlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
