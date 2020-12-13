import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConcordanceComponent } from './concordance.component';

describe('TabFormComponent', () => {
  let component: ConcordanceComponent;
  let fixture: ComponentFixture<ConcordanceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ConcordanceComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConcordanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
