import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WordStatusComponent } from './word-status.component';

describe('WordStatusComponent', () => {
  let component: WordStatusComponent;
  let fixture: ComponentFixture<WordStatusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WordStatusComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WordStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
