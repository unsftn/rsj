import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeterminantComponent } from './determinant.component';

describe('TabFormComponent', () => {
  let component: DeterminantComponent;
  let fixture: ComponentFixture<DeterminantComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DeterminantComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeterminantComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
