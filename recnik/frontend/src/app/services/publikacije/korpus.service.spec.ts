import { TestBed } from '@angular/core/testing';

import { KorpusService } from './korpus.service';

describe('KorpusService', () => {
  let service: KorpusService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(KorpusService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
