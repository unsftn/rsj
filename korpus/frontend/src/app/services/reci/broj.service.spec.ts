import { TestBed } from '@angular/core/testing';

import { BrojService } from './broj.service';

describe('BrojService', () => {
  let service: BrojService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BrojService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
