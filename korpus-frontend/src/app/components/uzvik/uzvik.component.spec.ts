import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UzvikComponent } from './uzvik.component';

describe('UzvikComponent', () => {
  let component: UzvikComponent;
  let fixture: ComponentFixture<UzvikComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UzvikComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UzvikComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
