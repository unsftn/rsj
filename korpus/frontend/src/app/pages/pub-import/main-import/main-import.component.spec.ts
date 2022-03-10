import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainImportComponent } from './main-import.component';

describe('MainImportComponent', () => {
  let component: MainImportComponent;
  let fixture: ComponentFixture<MainImportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MainImportComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MainImportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
