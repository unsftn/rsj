import { TestBed } from '@angular/core/testing';

import { ImenicaService } from './imenica.service';

describe('ImenicaService', () => {
  let service: ImenicaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImenicaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
