import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredlogComponent } from './predlog.component';

describe('PredlogComponent', () => {
  let component: PredlogComponent;
  let fixture: ComponentFixture<PredlogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PredlogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredlogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
