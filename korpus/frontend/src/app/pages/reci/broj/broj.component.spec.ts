import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrojComponent } from './broj.component';

describe('BrojComponent', () => {
  let component: BrojComponent;
  let fixture: ComponentFixture<BrojComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrojComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BrojComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
