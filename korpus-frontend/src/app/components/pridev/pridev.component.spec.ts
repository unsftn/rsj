import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PridevComponent } from './pridev.component';

describe('PridevComponent', () => {
  let component: PridevComponent;
  let fixture: ComponentFixture<PridevComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PridevComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PridevComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
