import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmeaningComponent } from './submeaning.component';

describe('TabFormComponent', () => {
  let component: SubmeaningComponent;
  let fixture: ComponentFixture<SubmeaningComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [SubmeaningComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubmeaningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
