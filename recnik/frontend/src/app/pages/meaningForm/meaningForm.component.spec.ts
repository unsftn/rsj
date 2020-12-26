import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MeaningFormComponent } from './meaningForm.component';

describe('TabFormComponent', () => {
  let component: MeaningFormComponent;
  let fixture: ComponentFixture<MeaningFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MeaningFormComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MeaningFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
