import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RendersComponent } from './renders.component';

describe('RendersComponent', () => {
  let component: RendersComponent;
  let fixture: ComponentFixture<RendersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RendersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RendersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
