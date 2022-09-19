import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MojeReciComponent } from './moje-reci.component';

describe('MojeReciComponent', () => {
  let component: MojeReciComponent;
  let fixture: ComponentFixture<MojeReciComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MojeReciComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MojeReciComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
