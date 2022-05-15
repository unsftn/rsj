import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReccaComponent } from './recca.component';

describe('ReccaComponent', () => {
  let component: ReccaComponent;
  let fixture: ComponentFixture<ReccaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReccaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReccaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
