import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AllWordsComponent } from './all-words.component';

describe('AllWordsComponent', () => {
  let component: AllWordsComponent;
  let fixture: ComponentFixture<AllWordsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AllWordsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AllWordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
