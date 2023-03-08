import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PossibleDupeComponent } from './possible-dupe.component';

describe('PossibleDupeComponent', () => {
  let component: PossibleDupeComponent;
  let fixture: ComponentFixture<PossibleDupeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PossibleDupeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PossibleDupeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
