import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GlagolComponent } from './glagol.component';

describe('GlagolComponent', () => {
  let component: GlagolComponent;
  let fixture: ComponentFixture<GlagolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GlagolComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GlagolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
