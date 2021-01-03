import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangesFormComponent } from './changesForm.component';

describe('TabFormComponent', () => {
  let component: ChangesFormComponent;
  let fixture: ComponentFixture<ChangesFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ChangesFormComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChangesFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
