import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectFilesComponent } from './select-files.component';

describe('SelectFilesComponent', () => {
  let component: SelectFilesComponent;
  let fixture: ComponentFixture<SelectFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SelectFilesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
