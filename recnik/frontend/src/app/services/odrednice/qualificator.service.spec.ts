import { TestBed } from '@angular/core/testing';

import { QualificatorService } from './qualificator.service';

describe('QualificatorService', () => {
  let service: QualificatorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(QualificatorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
