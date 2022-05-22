import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ZamenicaComponent } from './zamenica.component';

describe('ZamenicaComponent', () => {
  let component: ZamenicaComponent;
  let fixture: ComponentFixture<ZamenicaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ZamenicaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ZamenicaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
