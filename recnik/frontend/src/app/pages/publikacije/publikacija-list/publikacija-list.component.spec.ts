import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PublikacijaListComponent } from './publikacija-list.component';

describe('PublikacijaListComponent', () => {
  let component: PublikacijaListComponent;
  let fixture: ComponentFixture<PublikacijaListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PublikacijaListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PublikacijaListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
