import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VeznikComponent } from './veznik.component';

describe('VeznikComponent', () => {
  let component: VeznikComponent;
  let fixture: ComponentFixture<VeznikComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VeznikComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VeznikComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
