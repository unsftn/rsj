import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrojUnetihReciComponent } from './broj-unetih-reci.component';

describe('BrojUnetihReciComponent', () => {
  let component: BrojUnetihReciComponent;
  let fixture: ComponentFixture<BrojUnetihReciComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrojUnetihReciComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BrojUnetihReciComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
