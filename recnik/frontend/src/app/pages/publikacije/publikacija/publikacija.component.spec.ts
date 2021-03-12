import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PublikacijaComponent } from './publikacija.component';

describe('PublikacijeComponent', () => {
  let component: PublikacijaComponent;
  let fixture: ComponentFixture<PublikacijaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PublikacijaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PublikacijaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
