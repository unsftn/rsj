import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrilogComponent } from './prilog.component';

describe('PrilogComponent', () => {
  let component: PrilogComponent;
  let fixture: ComponentFixture<PrilogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PrilogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PrilogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
