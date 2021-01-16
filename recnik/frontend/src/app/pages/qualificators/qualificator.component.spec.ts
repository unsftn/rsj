import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QualificatorComponent } from './qualificator.component';

describe('TabFormComponent', () => {
  let component: QualificatorComponent;
  let fixture: ComponentFixture<QualificatorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [QualificatorComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QualificatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
