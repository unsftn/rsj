import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpressionsComponent } from './expressions.component';

describe('TabFormComponent', () => {
  let component: ExpressionsComponent;
  let fixture: ComponentFixture<ExpressionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ExpressionsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExpressionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
